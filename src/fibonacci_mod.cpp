#include <iostream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <string>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <cstdint>

// 使用64位整数处理大数
using int64 = int64_t;
using Pair = std::pair<int64, int64>;

// 自定义哈希函数用于pair
struct PairHash {
    size_t operator()(const Pair& p) const noexcept {
        return std::hash<int64>{}(p.first * 1000003ULL + p.second);
    }
};

// 比较两个pair
int comparePairs(const Pair& a, const Pair& b) {
    if (a.first != b.first) return (a.first < b.first) ? -1 : 1;
    if (a.second != b.second) return (a.second < b.second) ? -1 : 1;
    return 0;
}

// 找到最小循环的索引
size_t findMinCycleIndex(const std::vector<Pair>& cycle) {
    size_t minIdx = 0;
    for (size_t i = 1; i < cycle.size(); ++i) {
        if (comparePairs(cycle[i], cycle[minIdx]) < 0) {
            minIdx = i;
        }
    }
    return minIdx;
}

// 生成规范化的循环
std::vector<Pair> canonicalCycle(const std::vector<Pair>& cycle) {
    if (cycle.empty()) return {};
    
    size_t minIdx = findMinCycleIndex(cycle);
    std::vector<Pair> result;
    result.reserve(cycle.size());
    
    for (size_t i = 0; i < cycle.size(); ++i) {
        result.push_back(cycle[(minIdx + i) % cycle.size()]);
    }
    
    return result;
}

// 计算单个模数的所有周期
void computeModCycles(int64 base, std::vector<std::vector<int64>>& sequences, 
                     std::vector<std::vector<Pair>>& cyclesPairs) {
    if (base <= 0) return;
    
    std::unordered_set<Pair, PairHash> visited;
    visited.reserve(base * base * 2);
    
    std::vector<std::vector<Pair>> rawCycles;
    
    // 预分配空间
    const int64 totalPairs = base * base;
    visited.reserve(totalPairs * 2);
    
    // 进度显示（对于大模数）
    bool showProgress = (base > 1000);
    int64 progressInterval = std::max(int64(1), totalPairs / 100);
    
    for (int64 a0 = 0; a0 < base; ++a0) {
        for (int64 b0 = 0; b0 < base; ++b0) {
            Pair key = {a0, b0};
            if (visited.find(key) != visited.end()) continue;
            
            std::vector<Pair> path;
            std::unordered_map<Pair, size_t, PairHash> seenIndex;
            seenIndex.reserve(base * 2);
            
            Pair current = {a0, b0};
            
            // 限制迭代次数
            const size_t maxIterations = static_cast<size_t>(base) * base * 2 + 1000;
            size_t iterations = 0;
            
            while (iterations < maxIterations) {
                auto it = seenIndex.find(current);
                if (it != seenIndex.end()) {
                    // 找到循环起点
                    size_t start = it->second;
                    std::vector<Pair> cycle;
                    cycle.reserve(path.size() - start);
                    
                    for (size_t i = start; i < path.size(); ++i) {
                        cycle.push_back(path[i]);
                    }
                    
                    if (!cycle.empty()) {
                        rawCycles.push_back(canonicalCycle(cycle));
                    }
                    break;
                }
                
                seenIndex[current] = path.size();
                path.push_back(current);
                
                // 计算下一个状态
                int64 nextA = current.second;
                int64 nextB = (current.first + current.second) % base;
                current = {nextA, nextB};
                ++iterations;
            }
            
            // 标记路径中所有节点为已访问
            for (const auto& node : path) {
                visited.insert(node);
            }
            
            // 显示进度
            if (showProgress && (a0 * base + b0) % progressInterval == 0) {
                int64 progress = (a0 * base + b0) * 100 / totalPairs;
                std::cerr << "\r进度: " << progress << "%" << std::flush;
            }
        }
    }
    
    if (showProgress) {
        std::cerr << "\r进度: 100%" << std::endl;
    }
    
    // 去重
    std::unordered_set<std::string> seen;
    seen.reserve(rawCycles.size() * 2);
    
    for (const auto& cycle : rawCycles) {
        std::string key;
        key.reserve(cycle.size() * 16);
        for (const auto& p : cycle) {
            key += std::to_string(p.first);
            key += ",";
            key += std::to_string(p.second);
            key += ";";
        }
        
        if (seen.find(key) == seen.end()) {
            seen.insert(key);
            cyclesPairs.push_back(cycle);
            
            // 提取序列（第一个元素）
            std::vector<int64> seq;
            seq.reserve(cycle.size());
            for (const auto& p : cycle) {
                seq.push_back(p.first);
            }
            sequences.push_back(seq);
        }
    }
}

// 输出JSON格式
void outputJSON(int64 base, const std::vector<std::vector<int64>>& sequences,
                const std::vector<std::vector<Pair>>& cyclesPairs) {
    std::cout << "{" << std::endl;
    std::cout << "  \"base\": " << base << "," << std::endl;
    std::cout << "  \"sequence_count\": " << sequences.size() << "," << std::endl;
    std::cout << "  \"sequences\": [" << std::endl;
    
    for (size_t i = 0; i < sequences.size(); ++i) {
        std::cout << "    [";
        const auto& seq = sequences[i];
        for (size_t j = 0; j < seq.size(); ++j) {
            std::cout << seq[j];
            if (j < seq.size() - 1) std::cout << ", ";
        }
        std::cout << "]";
        if (i < sequences.size() - 1) std::cout << ",";
        std::cout << std::endl;
    }
    
    std::cout << "  ]," << std::endl;
    std::cout << "  \"cycles_pairs\": [" << std::endl;
    
    for (size_t i = 0; i < cyclesPairs.size(); ++i) {
        std::cout << "    [";
        const auto& cycle = cyclesPairs[i];
        for (size_t j = 0; j < cycle.size(); ++j) {
            std::cout << "[" << cycle[j].first << ", " << cycle[j].second << "]";
            if (j < cycle.size() - 1) std::cout << ", ";
        }
        std::cout << "]";
        if (i < cyclesPairs.size() - 1) std::cout << ",";
        std::cout << std::endl;
    }
    
    std::cout << "  ]" << std::endl;
    std::cout << "}" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "用法: " << argv[0] << " <模数> [输出文件]" << std::endl;
        std::cerr << "示例: " << argv[0] << " 1000" << std::endl;
        std::cerr << "      " << argv[0] << " 10000 > result.json" << std::endl;
        return 1;
    }
    
    int64 base = std::stoll(argv[1]);
    
    if (base <= 0) {
        std::cerr << "错误: 模数必须是正整数" << std::endl;
        return 1;
    }
    
    if (base > 1000000) {
        std::cerr << "警告: 模数 " << base << " 很大，计算可能需要较长时间..." << std::endl;
    }
    
    auto startTime = std::chrono::high_resolution_clock::now();
    
    std::vector<std::vector<int64>> sequences;
    std::vector<std::vector<Pair>> cyclesPairs;
    
    computeModCycles(base, sequences, cyclesPairs);
    
    auto endTime = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    
    std::cerr << "计算完成！" << std::endl;
    std::cerr << "模数: " << base << std::endl;
    std::cerr << "找到 " << sequences.size() << " 个不同的周期" << std::endl;
    std::cerr << "耗时: " << duration.count() << " 毫秒" << std::endl;
    
    // 输出JSON到stdout
    outputJSON(base, sequences, cyclesPairs);
    
    return 0;
}