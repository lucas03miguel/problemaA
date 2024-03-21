import sys
import random
import time

current = time.time()
random.seed(current)

def gerar_input_testes(T):
    input_gerado = f"{T}\n"
    
    for _ in range(T):
        R = random.randint(2, 5)  # Número de linhas
        C = random.randint(R, 5)  # Número de colunas, garantindo que R <= C
        M = random.randint(1, 7)  # Máximo de movimentos permitidos
        
        input_gerado += f"{R} {C} {M}\n"
        
        for _ in range(R):
            linha = [str(random.randint(1, R)) for _ in range(C)]
            input_gerado += ' '.join(linha) + "\n"
    
    return input_gerado

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <número de casos de teste>")
    else:
        T = int(sys.argv[1])
        inputs_gerados = gerar_input_testes(T)
        print(inputs_gerados)