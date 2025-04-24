print("Write your python code here. Write 'exit' if you want to leave...")
while True:
    kod = input(">>> ")
    if kod.lower() == 'exit':
        break
    try:
        exec(kod)
    except Exception as e:
        print("Error:", e)