#!/usr/bin/env node
/**
 * Kimi K3 独立识图脚本 - 调用 Moonshot Kimi K3 视觉模型（按量付费）。
 *
 * 用法:
 *   node vision.js <图片路径> [问题]
 *   node vision.js --url <图片链接> [问题]
 *
 * 说明:
 *   Kimi 官方接口不支持直接传公共图片 URL，因此 --url 模式会先把图片下载到
 *   内存，再转成 base64 发送。
 *
 * 配置（环境变量或同目录 .env 文件）:
 *   KIMI_API_KEY=sk-xxxx
 *   KIMI_BASE_URL=https://api.moonshot.cn/v1
 *   KIMI_VISION_MODEL=kimi-k3
 */

const fs = require("fs");
const path = require("path");
const https = require("https");
const http = require("http");

// ---- 最小 .env 加载（零第三方依赖）----
function loadEnv() {
  const envPath = path.join(__dirname, ".env");
  if (!fs.existsSync(envPath)) return;
  const text = fs.readFileSync(envPath, "utf8").replace(/^\uFEFF/, "");
  for (const line of text.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq === -1) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (!(key in process.env)) process.env[key] = value;
  }
}
loadEnv();

const BASE_URL = (process.env.KIMI_BASE_URL || "https://api.moonshot.cn/v1").replace(/\/+$/, "");
const API_KEY = process.env.KIMI_API_KEY || "";
const MODEL = process.env.KIMI_VISION_MODEL || "kimi-k3";

const MIME_MAP = {
  jpg: "jpeg", jpeg: "jpeg", png: "png", gif: "gif",
  webp: "webp", bmp: "bmp", heic: "heic", heif: "heif",
};

function parseArgs() {
  const argv = process.argv.slice(2);
  let imageSource = "", prompt = "", isUrl = false;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--url" && argv[i + 1]) {
      isUrl = true;
      imageSource = argv[++i];
    } else if (!imageSource && !argv[i].startsWith("--")) {
      imageSource = argv[i];
    } else if (imageSource && !argv[i].startsWith("--")) {
      prompt = prompt ? prompt + " " + argv[i] : argv[i];
    }
  }
  if (!prompt) prompt = "请详细描述这张图片的内容。";
  return { imageSource, prompt, isUrl };
}

function downloadBuffer(urlString) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlString);
    const transport = url.protocol === "https:" ? https : http;
    const req = transport.get(url, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return resolve(downloadBuffer(new URL(res.headers.location, url).href));
      }
      if (res.statusCode >= 400) {
        res.resume();
        return reject(new Error("下载图片失败，HTTP " + res.statusCode));
      }
      const chunks = [];
      res.on("data", (c) => chunks.push(c));
      res.on("end", () => resolve(Buffer.concat(chunks)));
    });
    req.on("error", reject);
    req.setTimeout(60000, () => req.destroy(new Error("下载图片超时")));
  });
}

async function resolveImageData(source, isUrl) {
  if (isUrl) {
    const buf = await downloadBuffer(source);
    const ext = path.extname(new URL(source).pathname).toLowerCase().replace(".", "");
    return "data:image/" + (MIME_MAP[ext] || "jpeg") + ";base64," + buf.toString("base64");
  }
  const resolved = path.resolve(source);
  if (!fs.existsSync(resolved)) throw new Error("文件不存在: " + resolved);
  const ext = path.extname(resolved).toLowerCase().replace(".", "");
  const data = fs.readFileSync(resolved);
  return "data:image/" + (MIME_MAP[ext] || "jpeg") + ";base64," + data.toString("base64");
}

function request(payload) {
  const url = new URL(BASE_URL + "/chat/completions");
  const body = JSON.stringify(payload);
  const transport = url.protocol === "https:" ? https : http;
  return new Promise((resolve, reject) => {
    const req = transport.request(url, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + API_KEY,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    }, (res) => {
      let data = "";
      res.on("data", (c) => data += c);
      res.on("end", () => {
        if (res.statusCode >= 400) {
          return reject(new Error("API " + res.statusCode + ": " + data.slice(0, 500)));
        }
        try {
          const json = JSON.parse(data);
          resolve(json.choices && json.choices[0] && json.choices[0].message
            ? json.choices[0].message.content
            : data);
        } catch { resolve(data); }
      });
    });
    req.on("error", reject);
    req.setTimeout(180000, () => req.destroy(new Error("请求超时")));
    req.write(body);
    req.end();
  });
}

async function main() {
  if (!API_KEY) {
    console.error("请设置 KIMI_API_KEY 环境变量，或在 " + path.join(__dirname, ".env") + " 中配置。");
    console.error("获取 Key: https://platform.moonshot.cn/console/api-keys");
    process.exit(1);
  }
  const { imageSource, prompt, isUrl } = parseArgs();
  if (!imageSource) {
    console.error("用法: node vision.js <图片路径> [问题]");
    console.error("      node vision.js --url <图片链接> [问题]");
    process.exit(1);
  }
  try {
    const imageData = await resolveImageData(imageSource, isUrl);
    const result = await request({
      model: MODEL,
      messages: [{
        role: "user",
        content: [
          { type: "image_url", image_url: { url: imageData } },
          { type: "text", text: prompt },
        ],
      }],
      stream: false,
    });
    console.log(result);
  } catch (err) {
    console.error("识图失败:", err.message);
    process.exit(1);
  }
}

main();