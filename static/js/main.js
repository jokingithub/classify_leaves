document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('leafImage'); // 获取文件输入元素
    var submitButton = document.getElementById('submitBtn'); // 获取开始识别按钮
    var selectedOption = document.querySelector('.custom-dropdown .selected-option'); // 获取下拉菜单的选中项
    var resultSectionShort = document.getElementById('shortPrediction'); // 获取简短结果区域
    var resultSectionDetail = document.getElementById('detailedPrediction'); // 获取详细结果区域

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

    // 监听开始识别按钮的点击事件
    submitButton.addEventListener('click', function() {
        var file = fileInput.files[0];
        var model = document.querySelector('.custom-dropdown .selected-option').textContent;

        if (!file) {
            alert('请先选择一张图片！');
            return;
        }

        // 处理图片上传
        handleImageUpload(file)
            .then(url => {
                // 创建 FormData 对象并添加数据
                var formData = new FormData();
                formData.append('leafImage', file);
                formData.append('model', model);

                // 发送数据到服务器
                return fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => response.json())
            .then(data => {
                // 解析并显示结果
                console.log(data)
                if (data && typeof data === 'object') {
                    resultSectionShort.textContent = data.name || '没有简短结果。';
                    resultSectionDetail.textContent = data.detailedDescription || '没有详细描述。';
                } else {
                    resultSectionShort.textContent = '返回的数据格式无效。';
                    resultSectionDetail.textContent = '';
                }
            })
            .catch(error => {
                resultSectionShort.textContent = '识别失败：' + error.message;
                resultSectionDetail.textContent = '';
                console.error('识别失败:', error);
            });
    });
});
