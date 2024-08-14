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
        var modelText = selectedOption.textContent.trim(); // 获取选中的文本内容
        var model;

        // 将选中的文本内容转换为服务器端识别的模型名称
        if (modelText === 'YOLOv8') {
            model = 'YOLO';
        } else if (modelText === 'ResNet50') {
            model = 'ResNet';
        } else {
            alert('请选择有效的模型！');
            return;
        }
        console.log(model)

        if (!file) {
            alert('请先选择一张图片！');
            return;
        }

        // 禁用按钮以防止重复点击
        submitButton.disabled = true;

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
            .then(response => {
                // 检查响应内容类型
                if (response.ok) {
                    return response.json(); // 尝试解析 JSON
                } else {
                    return response.text().then(text => {
                        throw new Error('服务器错误: ' + text);
                    });
                }
            })
            .then(data => {
                // 解析并显示结果
                console.log(data)
                if (data && typeof data === 'object') {
                    var name = data.name || '未定义名称';
                    var chineseName = data.chinese_name || '未定义中文名称';
                    var className = data.class !== undefined ? data.class : '未定义分类';
                    var confidence = data.confidence !== undefined ? data.confidence : '未定义置信度';
                    var description = data.description || '没有详细描述。';

                    resultSectionShort.innerHTML = `
                        <p><strong>名称:</strong> ${name}</p>
                        <p><strong>中文名称:</strong> ${chineseName}</p>
                        <p><strong>分类:</strong> ${className}</p>
                        <p><strong>置信度:</strong> ${confidence}</p>
                    `;

                    // 格式化描述内容
                    var formattedDescription = formatDescription(description);
                    resultSectionDetail.innerHTML = formattedDescription;
                } else {
                    resultSectionShort.textContent = '返回的数据格式无效。';
                    resultSectionDetail.textContent = '';
                }
            })
            .catch(error => {
                resultSectionShort.textContent = '识别失败：' + error.message;
                resultSectionDetail.textContent = '';
                console.error('识别失败:', error);
            })
            .finally(() => {
                // 重新启用按钮
                submitButton.disabled = false;
            });
        function formatDescription(description) {
        // 将换行符替换为 <br> 标签
        var formattedText = description.replace(/\n/g, '<br>');

        // 动态添加标题和列表（可选）
        formattedText = formattedText.replace(/基本信息：/g, '<h2>基本信息：</h2>');
        formattedText = formattedText.replace(/特征：/g, '<h2>特征：</h2>');
        formattedText = formattedText.replace(/分布：/g, '<h2>分布：</h2>');
        formattedText = formattedText.replace(/用途：/g, '<h2>用途：</h2>');

        // 将文本中的“特征：”、“分布：”等内容转换为段落
        formattedText = formattedText.replace(/(特征：|分布：|用途：)/g, '<p>$1</p>');
        formattedText = formattedText.replace(/(\d+)\./g, '<li>$1</li>');

        return formattedText;
    }
    });
});
