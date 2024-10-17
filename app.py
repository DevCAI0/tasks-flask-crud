# Importações necessárias do Flask
# Flask: O framework utilizado para criar a aplicação web
# request: Para acessar os dados da requisição (no caso, para receber o conteúdo de um POST)
# jsonify: Para retornar respostas JSON (estrutura de dados legível para a web)
from flask import Flask, request, jsonify

# Importa o modelo Task do arquivo models/task.py (assumindo que esse arquivo contém a definição da classe Task)
from models.task import Task

# Cria a instância da aplicação Flask
app = Flask(__name__)

# CRUD: Create (Criar), Read (Ler), Update (Atualizar) e Delete (Deletar)
# Essa aplicação realizará operações CRUD para gerenciar uma lista de tarefas

# Lista para armazenar as tarefas criadas
tasks = []

# Variável para controlar o ID das tarefas, garantindo que cada tarefa tenha um identificador único
task_id_control = 1

# Rota para criar uma nova tarefa (método POST)
# Essa rota recebe uma requisição JSON contendo os dados da tarefa (título e opcionalmente a descrição)
@app.route("/tasks/", methods=['POST'])
def create_task():
    global task_id_control  # Define o controle global para o ID da tarefa
    data = request.get_json()  # Extrai os dados enviados no corpo da requisição (formato JSON)

    # Cria uma nova tarefa usando os dados fornecidos
    # O ID é atribuído automaticamente usando o 'task_id_control'
    # O título é obrigatório, enquanto a descrição é opcional (padrão é uma string vazia)
    new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))

    # Incrementa o controle do ID para a próxima tarefa criada
    task_id_control += 1

    # Adiciona a nova tarefa à lista de tarefas
    tasks.append(new_task)

    # Retorna uma resposta JSON indicando que a tarefa foi criada com sucesso
    return jsonify({"message": "Nova tarefa criada com sucesso!"})

# Rota para listar todas as tarefas (método GET)
@app.route("/tasks/", methods=["GET"])
def get_tasks():
    # Cria uma lista de dicionários, onde cada tarefa é convertida para um formato legível (usando o método 'to_dict()' do modelo Task)
    task_list = [task.to_dict() for task in tasks]

    # Prepara o objeto de resposta JSON, contendo a lista de tarefas e o número total de tarefas
    output = {
        "tasks": task_list,  # Lista de tarefas convertida para JSON
        "total_tasks": len(task_list)  # Conta quantas tarefas estão na lista
    }

    # Retorna a resposta JSON com a lista de tarefas e o total
    return jsonify(output)

# Rota para listar tarefas pelo Id (método GET)
@app.route("/tasks/<int:id>", methods=["GET"])
def get_task_id(id):
    # Percorre a lista de tarefas para encontrar a tarefa com o ID fornecido
    for t in tasks:
        if t.id == id:
            # Retorna a tarefa encontrada no formato JSON
            return jsonify(t.to_dict())
    
    # Se a tarefa não for encontrada, retorna uma mensagem de erro e status 404
    return jsonify({"message": "Não foi possível encontrar essa tarefa"}), 404

# Rota para atualizar tarefas pelo Id (método PUT)
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    
    # Procura a tarefa correspondente ao id fornecido
    for t in tasks:
        if t.id == id:
            task = t
            break  # Sai do loop assim que a tarefa for encontrada

    # Se a tarefa não for encontrada, retorna um erro 404
    if task is None:
        return jsonify({"message": "Não foi possível encontrar essa tarefa"}), 404

    # Obtém os dados da requisição (esperado em formato JSON)
    data = request.get_json()

    # Atualiza os atributos da tarefa, usando o método `get` para evitar erros caso um campo não seja enviado
    task.title = data.get('title', task.title)  # Mantém o valor anterior se o novo não for fornecido
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    # Retorna uma mensagem de sucesso
    return jsonify({"message": "Tarefa atualizada com sucesso!"})


# Rota para deletar uma tarefa pelo Id (método DELETE)
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    # Inicializa a variável 'task' como None para armazenar a tarefa encontrada
    task = None
    
    # Percorre a lista de tarefas para encontrar a tarefa com o ID fornecido
    for t in tasks:
        if t.id == id:
            # Quando a tarefa é encontrada, atribui ela à variável 'task' e interrompe o loop
            task = t
            break  # Sai do loop assim que a tarefa é encontrada

    # Se a tarefa não for encontrada, retorna uma resposta 404 (não encontrado)
    if not task:
        return jsonify({"message": "Não foi possível encontrar essa tarefa"}), 404
    
    # Remove a tarefa da lista de tarefas
    tasks.remove(task)

    # Retorna uma mensagem de sucesso indicando que a tarefa foi deletada
    return jsonify({"message": "Tarefa deletada com sucesso!"})




   
# Ponto de entrada da aplicação Flask
# O app roda em modo de depuração para desenvolvimento (debug=True)
if __name__ == "__main__":
    app.run(debug=True)
