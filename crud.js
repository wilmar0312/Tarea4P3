if (localStorage.getItem('auth') !== 'true') {
  window.location.href = 'login.html';
}

const taskForm = document.getElementById('taskForm');
const taskInput = document.getElementById('taskInput');
const taskList = document.getElementById('taskList');
const logoutBtn = document.getElementById('logoutBtn');
const editTaskModal = new bootstrap.Modal(document.getElementById('editTaskModal'));
const editTaskInput = document.getElementById('editTaskInput');
const editTaskIndex = document.getElementById('editTaskIndex');
const saveEditBtn = document.getElementById('saveEditBtn');

let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function renderTasks() {
  taskList.innerHTML = '';
  tasks.forEach((task, index) => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-center';
    li.innerHTML = `
      <span>${task}</span>
      <div>
        <button class="btn btn-sm btn-primary me-2" onclick="openEditModal(${index})">Editar</button>
        <button class="btn btn-sm btn-danger" onclick="deleteTask(${index})">Eliminar</button>
      </div>
    `;
    taskList.appendChild(li);
  });
}

function openEditModal(index) {
  editTaskInput.value = tasks[index];
  editTaskIndex.value = index;
  editTaskModal.show();
}

function saveEditTask() {
  const index = parseInt(editTaskIndex.value);
  const newTask = editTaskInput.value.trim();
  if (newTask !== '') {
    tasks[index] = newTask;
    localStorage.setItem('tasks', JSON.stringify(tasks));
    renderTasks();
    editTaskModal.hide();
  }
}

function deleteTask(index) {
  tasks.splice(index, 1);
  localStorage.setItem('tasks', JSON.stringify(tasks));
  renderTasks();
}

taskForm.addEventListener('submit', function (e) {
  e.preventDefault();
  const newTask = taskInput.value.trim();
  if (newTask !== '') {
    tasks.push(newTask);
    localStorage.setItem('tasks', JSON.stringify(tasks));
    taskInput.value = '';
    renderTasks();
  }
});

saveEditBtn.addEventListener('click', saveEditTask);

logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('auth');
  window.location.href = 'login.html';
});

renderTasks();