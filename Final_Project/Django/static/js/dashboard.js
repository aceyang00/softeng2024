// 온도 및 습도 차트
const tempHumidityCtx = document.getElementById('tempHumidityChart').getContext('2d');
const tempHumidityChart = new Chart(tempHumidityCtx, {
    type: 'line',
    data: {
        labels: ['1시간 전', '50분 전', '40분 전', '30분 전', '20분 전', '10분 전', '현재'],
        datasets: [{
            label: '온도 (°C)',
            data: [22, 23, 23.5, 24, 23.5, 23, 22.5],
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            yAxisID: 'y-axis-temp',
        }, {
            label: '습도 (%)',
            data: [60, 58, 59, 61, 62, 60, 59],
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            yAxisID: 'y-axis-humidity',
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                id: 'y-axis-temp',
                type: 'linear',
                position: 'left',
                ticks: {
                    beginAtZero: false,
                    suggestedMin: 20,
                    suggestedMax: 30
                }
            }, {
                id: 'y-axis-humidity',
                type: 'linear',
                position: 'right',
                ticks: {
                    beginAtZero: false,
                    suggestedMin: 50,
                    suggestedMax: 70
                }
            }]
        }
    }
});

// 영양분 상태 차트
const nutrientCtx = document.getElementById('nutrientChart').getContext('2d');
const nutrientChart = new Chart(nutrientCtx, {
    type: 'radar',
    data: {
        labels: ['질소', '인', '칼륨', '칼슘', '마그네슘', '황'],
        datasets: [{
            label: '현재 영양분 수준',
            data: [65, 59, 90, 81, 56, 55],
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            pointBackgroundColor: 'rgb(54, 162, 235)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(54, 162, 235)'
        }]
    },
    options: {
        elements: {
            line: {
                borderWidth: 3
            }
        }
    }
});

// 생장 상태 업데이트
function updateGrowthStatus() {
    const growthStatus = document.getElementById('growthStatus');
    growthStatus.innerHTML = `
        <h4>현재 생장 단계: 영양 생장기</h4>
        <p>예상 수확일: 2024년 3월 15일</p>
        <p>생장률: 정상 (예상 대비 105%)</p>
    `;
}

// AI 추천 업데이트
function updateAIRecommendation() {
    const aiRecommendation = document.getElementById('aiRecommendation');
    aiRecommendation.innerHTML = `
        <h4>AI 추천 사항</h4>
        <ul>
            <li>수분 공급량을 10% 증가시키세요.</li>
            <li>다음 주 질소 비료 공급을 고려하세요.</li>
            <li>야간 온도를 2°C 낮추는 것이 좋습니다.</li>
        </ul>
    `;
}

// 페이지 로드 시 함수 실행
window.onload = function() {
    updateGrowthStatus();
    updateAIRecommendation();
};
