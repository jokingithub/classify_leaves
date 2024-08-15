document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('leafImage');
    var fileButton = document.querySelector('.custom-file-button');

    // 监听文件输入框的变化
    fileInput.addEventListener('change', function() {
        // 当用户选择了文件后，可以在这里更新按钮的文本或其他逻辑
        // 例如，显示文件名
        if (this.files && this.files.length > 0) {
            var fileName = this.files[0].name;
            fileButton.textContent = '已选择';
        }
    });
});