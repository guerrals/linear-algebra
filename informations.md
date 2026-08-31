# Resumo da Construção da Biblioteca `Matrix`

---

## Bloco 1: Estruturas Fundamentais e Álgebra Matricial

* **Estrutura de Dados e Operações Básicas:**
  * Implementação da classe `Matrix` baseada em listas bidimensionais (`data`).
  * Soma (`+`), Subtração (`-`) e Multiplicação por Escalar (`*`) com validação estrita de dimensões.
  * Transposição de matrizes ($A^T$) e Multiplicação Matricial ($A \times B$ ou `@`).
* **Determinante e Eliminação:**
  * Cálculo de Determinante por expansão em cofatores / redução para matrizes $2 \times 2$ e $3 \times 3$.
  * Algoritmo de Eliminação de Gauss-Jordan para conversão para a **Forma Escalonada Reduzida por Linhas (RREF)**.
  * Cálculo da **Matriz Inversa ($A^{-1}$)** através de RREF.

---

## Bloco 2: Sistemas Lineares, Aproximações e Testes

* **Resolução de Sistemas Lineares (`solve`):**
  * Solução de sistemas $Ax = B$ via matriz aumentada e RREF.
  * Classificação de sistemas em Solução Única (SPD) e Soluções Infinitas (SPI).
* **Regressão e Mínimos Quadrados (`least_squares`):**
  * Implementação da equação normal $X = (A^T A)^{-1} A^T B$ para encontrar a melhor reta de ajuste em dados ruidosos.
  * Integração da aproximação no método `.solve()` como um *fallback* inteligente para tratar Sistemas Impossíveis (SI).
* **Infraestrutura de Testes:**
  * Migração da suíte de testes customizada para o framework padrão do Python (`unittest`).
  * Validação de tolerância decimal via `assertMatrixAlmostEqual` e captura de exceções via `assertRaises`.

---

## Bloco 3: Transição para Espaços Vetoriais

* **Posto de uma Matriz (`rank`):**
  * Contagem de linhas não nulas na RREF para determinar o número de dimensões efetivas do espaço gerado pelas linhas/colunas.
* **Independência Linear (`is_linearly_independent`):**
  * Algoritmo para classificar conjuntos de vetores como Linearmente Independente (LI) ou Dependente (LD), checando se $\text{rank}(A) = k$ (número de vetores).
* **Alinhamento Acadêmico:**
  * Mapeamento direto das rotinas computacionais com os livros da disciplina (*Callioli* e *Anton & Rorres*) para suportar os tópicos de Subespaços, Base, Dimensão e Núcleo.


# Guia de Algoritmos e Operações Matriciais

---

## 1. Operações Elementares e Álgebra Básica

* **Soma e Subtração ($A \pm B$):**
  1. Verifica se $A$ e $B$ possuem as mesmas dimensões ($m \times n$).
  2. Percorre cada elemento e executa $C_{i,j} = A_{i,j} \pm B_{i,j}$.

* **Multiplicação por Escalar ($k \cdot A$):**
  1. Percorre a matriz multiplicando cada posição por $k$: $C_{i,j} = k \cdot A_{i,j}$.

* **Transposição ($A^T$):**
  1. Para uma matriz $m \times n$, cria uma matriz destino de dimensão $n \times m$.
  2. Inverte os índices de cada elemento: $(A^T)_{j,i} = A_{i,j}$.

* **Multiplicação Matricial ($A \times B$):**
  1. Verifica a compatibilidade: o número de colunas de $A$ deve ser igual ao número de linhas de $B$.
  2. Para cada linha $i$ de $A$ e cada coluna $j$ de $B$, calcula o produto escalar:
     $$C_{i,j} = \sum_{k=1}^{n} A_{i,k} \cdot B_{k,j}$$

---

## 2. Escalonamento e Eliminação de Gauss-Jordan (RREF)

A Forma Escalonada Reduzida por Linhas (**RREF**) é o motor computacional da biblioteca. O algoritmo opera aplicando as três **Operações Elementares nas Linhas**:
1. Trocar duas linhas de posição.
2. Multiplicar uma linha por um escalar não nulo.
3. Somar a uma linha o múltiplo de outra linha.

### Passo a Passo do Algoritmo Gauss-Jordan

1. **Inicialização do Ponteiro:**
   * Define `pivot_row = 0`.

2. **Iteração sobre as Colunas ($j = 0 \dots n-1$):**
   * **Passo 1 — Busca do Pivô:** Procura um elemento não nulo na coluna $j$, a partir da linha `pivot_row` para baixo.
   * **Passo 2 — Pivoteamento Parcial:** Encontra a linha com o maior valor absoluto na coluna $j$ (para minimizar erros de ponto flutuante) e troca essa linha com a `pivot_row`.
   * **Passo 3 — Trata Coluna Nula:** Se todos os elementos da coluna $j$ abaixo/na `pivot_row` forem zero, pula para a próxima coluna sem incrementar `pivot_row`.
   * **Passo 4 — Normalização do Pivô:** Divide toda a linha `pivot_row` pelo valor do pivô $P$, garantindo que a entrada do pivô se torne $1$:
     $$L_{\text{pivot}} \leftarrow \frac{L_{\text{pivot}}}{P}$$
   * **Passo 5 — Zerar a Coluna (Eliminação Acima e Abaixo):** Para cada linha $r$ da matriz (exceto a `pivot_row`):
     * Determina o fator $F = A_{r,j}$.
     * Subtrai o múltiplo da linha pivô da linha $r$:
       $$L_r \leftarrow L_r - (F \cdot L_{\text{pivot}})$$
   * **Passo 6 — Avançar:** Incrementa `pivot_row = pivot_row + 1`. Se `pivot_row` atingir o total de linhas, encerra.

---

## 3. Resolução de Sistemas Lineares (`solve`)

1. **Montagem da Matriz Aumentada $[A | B]$:** Concatena os vetores das constantes $B$ à direita da matriz de coeficientes $A$.
2. **Aplicação do Gauss-Jordan:** Executa o algoritmo RREF na matriz aumentada $[A | B]$.
3. **Análise de Consistência (Teorema de Rouché-Capelli):**
   * **Sistema Impossível (SI):** Se surgir qualquer linha onde a parte dos coeficientes seja toda nula e a constante correspondente seja diferente de zero ($[0 \dots 0 \mid c]$ com $c \neq 0$), aciona o *fallback* para Mínimos Quadrados.
   * **Sistema Possível Indeterminado (SPI):** Se o número de linhas não nulas for menor que o número de variáveis ($\text{posto} < n$), dispara `ValueError` indicando soluções infinitas.
   * **Sistema Possível Determinado (SPD):** Se a parte dos coeficientes se reduzir à Identidade, extrai a última coluna como a solução única.

---

## 4. Mínimos Quadrados (`least_squares`)

Utilizado em dados ruidosos ou como *fallback* para Sistemas Impossíveis ($Ax = B$).

1. **Calcula a Transposta:** Obtém $A^T$.
2. **Forma as Equações Normais:**
   * Calcula a matriz de covariância: $M = A^T A$.
   * Calcula o vetor projetado: $V = A^T B$.
3. **Inversão e Solução:**
   * Inverte a matriz $M$: $M^{-1} = (A^T A)^{-1}$.
   * Multiplica pela projeção: $X = M^{-1} \cdot V$.

---

## 5. Matriz Inversa (`inverse`)

1. **Verificação de Matriz Quadrada:** Garante que a matriz possui dimensões $n \times n$.
2. **Verificação do Determinante:** Se $\det(A) = 0$, a matriz é singular e dispara `ValueError`.
3. **Montagem da Matriz Aumentada $[A | I_n]$:** Concatena a Matriz Identidade de mesma dimensão à direita de $A$.
4. **Redução por Gauss-Jordan:** Aplica o RREF em todo o conjunto $[A | I_n]$.
5. **Extração:** Após a conversão do lado esquerdo na Identidade, o lado direito é a matriz inversa $A^{-1}$.

---

## 6. Espaços Vetoriais: Posto e Independência Linear

### Posto (`rank`)
1. Aplica RREF na matriz.
2. Percorre as linhas do resultado e conta quantas possuem ao menos um elemento diferente de zero (com tolerância $10^{-7}$).
3. O total de linhas não nulas é o **Posto**.

### Independência Linear (`is_linearly_independent`)
1. Recebe um conjunto de $k$ vetores de dimensão $n$.
2. Monta uma matriz $A_{n \times k}$ posicionando os vetores como **colunas**.
3. Calcula o posto $r = \text{rank}(A)$.
4. **Decisão:** Se $r = k$, os vetores são **LI**. Se $r < k$, são **LD**.