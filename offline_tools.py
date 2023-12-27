def plot_results(results_list, bottom=0, top=1, marker='o'):
    from matplotlib import pyplot
    # 繪製標準化後的數據，並添加標記以顯示每個點
    pyplot.plot(results_list, marker=marker)
    # 繪製 y = 0.5 的線
    pyplot.axhline(y=0.5, color='r', linestyle='-')
    pyplot.ylim(bottom, top)
    # 顯示圖表
    pyplot.show()