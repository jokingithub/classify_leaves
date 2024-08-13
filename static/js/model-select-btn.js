document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.custom-dropdown');
    var selectedOption = dropdown.querySelector('.selected-option');
    var optionsList = dropdown.querySelector('.options-list');
    var options = optionsList.querySelectorAll('li');

    // 处理下拉菜单的显示和隐藏
    dropdown.addEventListener('click', function(event) {
        // 仅当点击的是下拉按钮本身时才切换下拉菜单的显示状态
        if (event.target === dropdown) {
            dropdown.classList.toggle('open');
        }
    });

    // 处理选项点击事件
    options.forEach(function(option) {
        option.addEventListener('click', function() {
            // 更新选中的文本
            selectedOption.textContent = option.textContent;
            // 可以在这里添加额外的逻辑，例如更新数据模型等
            // 例如: updateDataModel(option.dataset.value);
            // 关闭下拉菜单
            dropdown.classList.remove('open');
            event.stopPropagation(); // 阻止事件继续传播
        });
    });

    // 点击外部时关闭下拉菜单
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove('open');
            optionsList.classList.remove('visible'); // 确保下拉列表隐藏
        }
    });
});