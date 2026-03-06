const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// public 폴더의 정적 파일(HTML, CSS 등)을 서비스합니다.
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.send('Hello, World! My first server is running.');
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});