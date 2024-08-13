document.addEventListener('DOMContentLoaded', function() {
    var uploadedImage = document.getElementById('uploadedImage'); // 获取图片显示元素
    var fileInput = document.getElementById('leafImage'); // 获取文件输入元素

    // 处理图片上传并返回图片的 Data URL
    function handleImageUpload(file) {
        var reader = new FileReader();

        return new Promise((resolve, reject) => {
            reader.onload = function(event) {
                resolve(event.target.result);
            };
            reader.onerror = function() {
                reject(new Error('图片读取失败'));
            };
            reader.readAsDataURL(file);
        });
    }

    // 监听文件输入变化事件
    fileInput.addEventListener('change', function(event) {
        var file = event.target.files[0];
        if (file) {
            handleImageUpload(file)
                .then(url => {
                    uploadedImage.src = url; // 更新图片的 src 属性
                    uploadedImage.style.display = 'block'; // 确保图片显示
                })
                .catch(error => {
                    console.error('图片读取失败:', error);
                });
        }
    });
});
