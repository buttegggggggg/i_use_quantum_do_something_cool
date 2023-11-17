def common_terms():
    from qiskit import QuantumCircuit, Aer, transpile, IBMQ
    from qiskit.tools.monitor import job_monitor


    # Load the saved IBM Q account
    IBMQ.load_account()

    # Get the provider
    provider = IBMQ.get_provider()

    # Select a quantum hardware backend
    # available_backends = provider.backends(filters=lambda x: x.configuration().n_qubits >= 1 and not x.configuration().simulator)
    backend = provider.backends.ibm_lagos # least_busy(available_backends)
    print(f"Using {backend.name()}")

    # 創建一個量子電路
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # 添加 H-gate
    qc.measure([0], [0])

    # 編譯電路
    compiled_circuit = transpile(qc,  backend=backend, optimization_level=3)


    results_list = []

    # 迴圈 n=1 ~ 10000
    for n in range(1, 4):
        # 執行模擬
        job =  backend.run(compiled_circuit, shots=n)
        result = job.result()
        counts = result.get_counts(qc)
        
        # 獲取結果為 0 的次數並除以 n
        zero_counts = counts.get('0', 0)
        ratio = zero_counts / n
        results_list.append(ratio)
        
        # 打印結果列=f
        print(results_list)
