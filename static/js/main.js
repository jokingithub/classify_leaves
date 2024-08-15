document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('leafImage');
    var submitButton = document.getElementById('submitBtn');
    var selectedOption = document.querySelector('.custom-dropdown .selected-option');
    var resultSectionShort = document.getElementById('shortPrediction');
    var resultSectionDetail = document.getElementById('detailedPrediction');
    var loadingIndicator = document.getElementById('loadingIndicator'); // 获取加载动画容器

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

    function showLoadingIndicator() {
        loadingIndicator.style.display = 'flex'; // 显示加载动画
    }

    function hideLoadingIndicator() {
        loadingIndicator.style.display = 'none'; // 隐藏加载动画
    }

    function formatDescription(description) {
        return description.replace(/\n/g, '<br>');
    }

    function handleError(response) {
        if (response.ok) {
            return response.json();
        } else {
            return response.text().then(text => {
                throw new Error('服务器错误: ' + text);
            });
        }
    }

    submitButton.addEventListener('click', function() {
        var file = fileInput.files[0];
        var modelText = selectedOption.textContent.trim();
        var model;

        if (modelText === 'YOLOv8') {
            model = 'YOLO';
        } else if (modelText === 'ResNet50') {
            model = 'ResNet';
        } else {
            alert('请选择有效的模型！');
            return;
        }

        if (!file) {
            alert('请先选择一张图片！');
            return;
        }

        if (!file.type.startsWith('image/')) {
            alert('请选择一个有效的图片文件！');
            return;
        }

        submitButton.disabled = true;
        showLoadingIndicator();

        handleImageUpload(file)
            .then(url => {
                var formData = new FormData();
                formData.append('leafImage', file);
                formData.append('model', model);

                return fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(handleError)
            .then(predictionData => {
                var name = predictionData.name || '未定义名称';
                var chineseName = predictionData.chinese_name || '未定义中文名称';
                var className = predictionData.class !== undefined ? predictionData.class : '未定义分类';
                var confidence = predictionData.confidence !== undefined ? predictionData.confidence : '未定义置信度';
                var description = predictionData.description || '没有详细描述。';

                resultSectionShort.innerHTML = `
                    <p><strong>名称:</strong> ${name}</p>
                    <p><strong>中文名称:</strong> ${chineseName}</p>
                    <p><strong>分类:</strong> ${className}</p>
                    <p><strong>置信度:</strong> ${confidence}</p>
                `;

                var formattedDescription = formatDescription(description);
                resultSectionDetail.innerHTML = formattedDescription;
            })
            .catch(error => {
                resultSectionShort.textContent = '识别失败：' + error.message;
                resultSectionDetail.textContent = '';
                console.error('识别失败:', error);
            })
            .finally(() => {
                hideLoadingIndicator();
                submitButton.disabled = false;
            });
    });
});
