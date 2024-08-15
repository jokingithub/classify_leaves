document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.custom-dropdown');
    var optionsList = dropdown.querySelector('.options-list');
    var selectedOption = dropdown.querySelector('.selected-option');

    // 检测屏幕宽度变化
    function updateDropdownInteraction() {
        if (window.innerWidth < 1024) {
            // 移动端交互逻辑：点击显示和隐藏下拉列表
            dropdown.removeEventListener('mouseenter', showDropdown);
            dropdown.removeEventListener('mouseleave', hideDropdown);

            dropdown.addEventListener('click', toggleDropdown);
            document.addEventListener('click', closeDropdownOnClickOutside);
        } else {
            // 桌面端交互逻辑：悬停显示下拉列表
            dropdown.addEventListener('mouseenter', showDropdown);
            dropdown.addEventListener('mouseleave', hideDropdown);

            dropdown.removeEventListener('click', toggleDropdown);
            document.removeEventListener('click', closeDropdownOnClickOutside);
        }
    }

    function showDropdown() {
        optionsList.classList.add('visible');
    }

    function hideDropdown() {
        optionsList.classList.remove('visible');
    }

    function toggleDropdown(event) {
        optionsList.classList.toggle('visible');
        event.stopPropagation(); // 防止事件冒泡
    }

    function closeDropdownOnClickOutside(event) {
        if (!dropdown.contains(event.target)) {
            optionsList.classList.remove('visible');
        }
    }

    // 处理选项点击事件
    var options = optionsList.querySelectorAll('li');
    options.forEach(function(option) {
        option.addEventListener('click', function(event) {
            selectedOption.textContent = option.textContent;
            // 更新选中项后，隐藏下拉菜单
            optionsList.classList.remove('visible');
            dropdown.classList.remove('open'); // 确保下拉菜单完全关闭
            event.stopPropagation(); // 防止关闭时冒泡引发其他事件
        });
    });

    // 初始加载时调用一次，确保交互逻辑与屏幕宽度一致
    updateDropdownInteraction();

    // 监听窗口尺寸变化
    window.addEventListener('resize', updateDropdownInteraction);

    // 在选项列表之外的点击关闭下拉菜单
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target)) {
            optionsList.classList.remove('visible');
        }
    });
});
