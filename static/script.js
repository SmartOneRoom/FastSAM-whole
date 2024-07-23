document.addEventListener('DOMContentLoaded', function() {
    const webcamFeed = document.getElementById('webcamFeed');
    const segmentation = document.getElementById('segmentation');
    const toggleButton = document.getElementById('toggleButton');

    // 웹캠 피드 URL 설정
    webcamFeed.src = '/video_feed';

    // 세그멘테이션 이미지 피드 URL 설정
    segmentation.src = '/segmentation_feed';
    
    // 세그멘테이션 초기 상태 숨김
    segmentation.style.display = 'none';

    // 버튼 상태 관리
    let isSegmentationVisible = false;

    toggleButton.addEventListener('click', function() {
        if (isSegmentationVisible) {
            segmentation.style.display = 'none';
            toggleButton.textContent = 'Start Segmentation';
            toggleButton.classList.remove('stop');
        } else {
            segmentation.style.display = 'block';
            toggleButton.textContent = 'Stop Segmentation';
            toggleButton.classList.add('stop');
        }
        isSegmentationVisible = !isSegmentationVisible;
    });
});
