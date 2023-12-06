from qiskit import QuantumCircuit, transpile, IBMQ, providers
from qiskit.providers import ibmq

def plot_results(results_list):
    from matplotlib import pyplot
    # 繪製標準化後的數據，並添加標記以顯示每個點
    pyplot.plot(results_list, marker='o')
    # 繪製 y = 0.5 的線
    pyplot.axhline(y=0.5, color='r', linestyle='-')
    pyplot.ylim(0, 1)
    # 顯示圖表
    pyplot.show()

class IBMQ_backends:
    IBMQ.load_account()
    provider = IBMQ.get_provider()

    @classmethod
    def ibm_lagos(cls):
        return cls.provider.backends.ibm_lagos

    @classmethod
    def least_busy(cls):
        return ibmq.least_busy(cls.provider.backends(simulator = False))
    
    @classmethod
    def simulator(cls):
        return ibmq.least_busy(cls.provider.backends(simulator = True))

def run_circuits(start, stop, get_backend, show_plot, each_shot=False):
    """創建一個量子電路

    1 1 1 1 1 1 1 ...  -> [[[[[[[[1] 2] 3] 4] 5] 6] 7] 
      2 2 2 2 2 2
        3 3 3 3 3
          4 4 4 4
            5 5 5
              6 6
                7
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # 添加 H-gate
    qc.measure([0], [0])
    results_list=[]
    if each_shot:
        results_ratio = []
    for n in range(start, stop):
        from backoff import on_exception, expo
        @on_exception(expo, ibmq.job.IBMQJobApiError)
        def run_circuit():
            backend = get_backend()
            print(f"Using {backend.name()}")
            # 獲取結果為 0 的次數並除以 n
            result = backend.run(transpile(qc,  backend=backend, optimization_level=3), shots=n, memory=each_shot).result()
            # 增加 memory=each_shot （每次結果都記錄，並非僅記錄次數）

            def 打印結果列(results_list):
                print('n =', len(results_list))
                print(results_list)
                if show_plot:
                    plot_results(results_list)
            if each_shot:
                for shot_result in result.get_memory():
                    results_list.append((results_list[-1] if results_list else 0) + int(shot_result))
                    results_ratio.append(results_list[-1] / len(results_list))
                    打印結果列(results_ratio)
            else:
                results_list.append(result.get_counts(qc).get('0', 0) / n)
                打印結果列(results_list)
        run_circuit()

def run_circuits(start, stop, get_backend):
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # 添加 H-gate
    qc.measure([0], [0])

    n = int(stop)
    
    result_list = []
    
    backend = get_backend()
    print(f"Using {backend.name()}")
   
    result = backend.run(transpile(qc,  backend=backend ,optimization_level=3),  shots=n, memory=True).result()
    
    # 獲得每次測量的結果
    measurement_results = result.get_memory()
    print('measurement results =' ,measurement_results)
    for i in range(start-1, stop):
        ith_list = measurement_results[start-1 : i+1]
        ith_0_num = ith_list.count('0')
        ith_0_prob = ith_0_num/(i+1)

        #print(ith_list,ith_0_num,ith_0_prob )
        result_list.append(ith_0_prob)
    print('probability of 0 =',result_list)
    plot_results(result_list)