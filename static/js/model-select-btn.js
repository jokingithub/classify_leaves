document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.custom-dropdown');
    var optionsList = dropdown.querySelector('.options-list');

    // 鼠标移入下拉按钮时显示下拉菜单
    dropdown.addEventListener('mouseenter', function() {
        optionsList.classList.add('visible');
    });

    // 鼠标移出下拉按钮时隐藏下拉菜单
    dropdown.addEventListener('mouseleave', function() {
        optionsList.classList.remove('visible');
    });

    // 处理选项点击事件
    var options = optionsList.querySelectorAll('li');
    var selectedOption = dropdown.querySelector('.selected-option');
    options.forEach(function(option) {
        option.addEventListener('click', function() {
            selectedOption.textContent = option.textContent;
            // 更新选中项后，隐藏下拉菜单
            optionsList.classList.remove('visible');
        });
    });
});