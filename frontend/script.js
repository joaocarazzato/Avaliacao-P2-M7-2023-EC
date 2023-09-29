var server_ip = "localhost:8000"

function addTask() {
  const taskInput = document.getElementById("taskInput");
  const taskText = taskInput.value.trim();

  if (taskText !== "") {
    //Realizar um POST com fetch para enviar os dados para o backend
    fetch(`http://${server_ip}/create_note`, {
      method: "POST",
      body: JSON.stringify({
        titulo: `Minha Nota`,
        descricao: `${taskText}`,
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => response.json())
      .then((json) => {
        getTasks();
      });
  }
  taskInput.value = "";
}

function getTasks() {
  const taskList = document.getElementById("taskList");
  //Limpa a lista
  taskList.innerHTML = "";
  fetch(`http://${server_ip}/notes`)
    .then((response) => response.json())
    .then((data) => {
      data["data"].forEach((task) => {
        const newTaskItem = document.createElement("li");

        // Criar elemento de texto da tarefa
        const taskTextElement = document.createElement("span");
        taskTextElement.textContent = `${task[1]} : ${task[2]}  `;
        newTaskItem.appendChild(taskTextElement);

        // Botão para excluir a tarefa
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Excluir";
        deleteButton.addEventListener("click", function () {
          deleteTask(task[0]);
          taskList.removeChild(newTaskItem);
        });

        newTaskItem.appendChild(deleteButton);

        // Adicionar a nova tarefa à lista
        taskList.appendChild(newTaskItem);
      });
    })
    .catch((error) => {
      console.error("Erro:", error);
    });
}

function deleteTask(id){
  fetch(`http://${server_ip}/delete_note/`, {
    method: "DELETE",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
    body: JSON.stringify({id: id})
  })
    .then((response) => response.json())
    .then((json) => {
      getTasks();
    });
}