const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, '../public')));

// [새로 추가된 코드] 서버의 현재 상태와 시간을 알려주는 창구(API)입니다.
app.get('/api/status', (req, res) => {
  res.json({
    message: "서버가 아주 건강하게 작동 중입니다!",
    serverTime: new Date().toLocaleString('ko-KR'),
    owner: "병각님"
  });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});