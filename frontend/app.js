// 前端与后端同源部署时留空；若把前端单独起在别的端口，改成 "http://localhost:5000"。
const API_BASE = "";

const CELL_SIZE = 32;
const DIRECTION_LABELS = { N: "北（向上）", E: "东（向右）", S: "南（向下）", W: "西（向左）" };
const STATUS_LABELS = { idle: "待机", moving: "移动中", blocked: "受阻" };
const ARROW_ANGLES = { N: -Math.PI / 2, E: 0, S: Math.PI / 2, W: Math.PI };

let mapData = null;
let robotState = null;

const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");
const messageBox = document.getElementById("message");
const allButtons = Array.from(document.querySelectorAll("button"));

async function request(path, options) {
  const response = await fetch(`${API_BASE}${path}`, options);
  if (!response.ok) {
    let detail = `请求失败（HTTP ${response.status}）`;
    try {
      const body = await response.json();
      if (body.error) detail = body.error;
    } catch (_) {
      // 响应不是 JSON，保留默认提示。
    }
    throw new Error(detail);
  }
  return response.json();
}

function showMessage(text, isBlocked = false) {
  messageBox.textContent = text;
  messageBox.classList.toggle("blocked", isBlocked);
}

function sizeCanvas() {
  canvas.width = mapData.width * CELL_SIZE;
  canvas.height = mapData.height * CELL_SIZE;
}

function drawMap() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#e3e8ee";
  ctx.lineWidth = 1;
  for (let col = 0; col <= mapData.width; col += 1) {
    const x = col * CELL_SIZE + 0.5;
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  for (let row = 0; row <= mapData.height; row += 1) {
    const y = row * CELL_SIZE + 0.5;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }

  ctx.fillStyle = "#8c9bab";
  for (const [x, y] of mapData.obstacles) {
    ctx.fillRect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2);
  }

  ctx.strokeStyle = "#5b6b7c";
  ctx.lineWidth = 2;
  ctx.strokeRect(1, 1, canvas.width - 2, canvas.height - 2);
}

function drawRobot() {
  const centerX = robotState.x * CELL_SIZE + CELL_SIZE / 2;
  const centerY = robotState.y * CELL_SIZE + CELL_SIZE / 2;

  ctx.beginPath();
  ctx.arc(centerX, centerY, CELL_SIZE * 0.32, 0, Math.PI * 2);
  ctx.fillStyle = robotState.status === "blocked" ? "#b42318" : "#d24b3e";
  ctx.fill();

  const angle = ARROW_ANGLES[robotState.direction];
  const tipX = centerX + Math.cos(angle) * CELL_SIZE * 0.26;
  const tipY = centerY + Math.sin(angle) * CELL_SIZE * 0.26;
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(centerX, centerY);
  ctx.lineTo(tipX, tipY);
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(tipX, tipY, 2.5, 0, Math.PI * 2);
  ctx.fillStyle = "#ffffff";
  ctx.fill();
}

function render() {
  if (!mapData || !robotState) return;
  drawMap();
  drawRobot();
  document.getElementById("stateX").textContent = robotState.x;
  document.getElementById("stateY").textContent = robotState.y;
  document.getElementById("stateDirection").textContent =
    DIRECTION_LABELS[robotState.direction] || robotState.direction;
  document.getElementById("stateStatus").textContent =
    STATUS_LABELS[robotState.status] || robotState.status;
}

async function sendCommand(command) {
  allButtons.forEach((button) => { button.disabled = true; });
  try {
    robotState = await request("/api/robot/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command }),
    });
    render();
    if (robotState.status === "blocked") {
      showMessage("前方越界或遇到障碍物，机器人已停在原地。", true);
    } else {
      showMessage(`指令已执行，当前状态：${STATUS_LABELS[robotState.status]}。`);
    }
  } catch (error) {
    showMessage(`操作失败：${error.message}`, true);
  } finally {
    allButtons.forEach((button) => { button.disabled = false; });
  }
}

async function loadInitialState() {
  try {
    [mapData, robotState] = await Promise.all([
      request("/api/map"),
      request("/api/robot"),
    ]);
    sizeCanvas();
    render();
    showMessage("已连接后端，可以开始控制。");
  } catch (error) {
    showMessage(`连接后端失败：${error.message}`, true);
  }
}

document.getElementById("turnLeftBtn").addEventListener("click", () => sendCommand("left"));
document.getElementById("forwardBtn").addEventListener("click", () => sendCommand("forward"));
document.getElementById("turnRightBtn").addEventListener("click", () => sendCommand("right"));
document.getElementById("resetBtn").addEventListener("click", () => sendCommand("reset"));

loadInitialState();

// 定时同步，保证页面显示与 API 返回一致。
setInterval(async () => {
  try {
    const latest = await request("/api/robot");
    if (JSON.stringify(latest) !== JSON.stringify(robotState)) {
      robotState = latest;
      render();
    }
  } catch (_) {
    // 轮询失败不打断当前操作，下次再试。
  }
}, 2000);
