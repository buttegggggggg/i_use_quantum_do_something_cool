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

def run_circuits(start, stop, get_backend, show_plot):
    # 創建一個量子電路
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # 添加 H-gate
    qc.measure([0], [0])
    results_list=[]
    for n in range(start, stop):
        from backoff import on_exception, expo
        @on_exception(expo, ibmq.job.IBMQJobApiError)
        def run_circuit():
            backend = get_backend()
            print(f"Using {backend.name()}")
            # 獲取結果為 0 的次數並除以 n
            results_list.append(backend.run(
                transpile(qc,  backend=backend, optimization_level=3), 
                shots=n).result().get_counts(qc).get('0', 0) / n)
            print('n =', n)
            # 打印結果列=f
            print(results_list)
            if show_plot:
                plot_results(results_list)
        run_circuit()