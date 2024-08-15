document.addEventListener("DOMContentLoaded", function() {
    fetchCategories();
});

function fetchCategories() {
    fetch('/categories')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#categoryTable tbody');
            console.log(tableBody);
            tableBody.innerHTML = '';  // 清空表格内容
            data.forEach(category => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${category.id}</td>
                    <td>${category.category_name}</td>
                    <td>${category.chinese_name}</td>
                    <td>${category.description}</td>
                    <td>
                        <button onclick="editCategory(${category.id})">编辑</button>
                        <button onclick="deleteCategory(${category.id})">删除</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });
}

function editCategory(id) {
    // 处理编辑类别的逻辑
}

function deleteCategory(id) {
    // 发送删除请求
    fetch(`/delete_category/${id}`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            fetchCategories();  // 重新获取类别列表
        }
    });
}

function exportFeedback() {
    window.location.href = '/export_feedback';
}