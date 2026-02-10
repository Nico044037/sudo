const { Client, GatewayIntentBits } = require("discord.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const TOKEN = "YOUR_BOT_TOKEN";

// USERS WHO CAN ACTUALLY SUDO
const SUDO_USERS = ["123456789012345678"];

// FAKE FILE SYSTEM
let currentDir = "/";
let files = {
  "/": ["home", "etc", "root", "virus.exe"],
  "/home": ["beluga", "notes.txt"],
  "/home/beluga": ["secret.txt"],
};

// COMMAND HANDLER
client.on("messageCreate", async (msg) => {
  if (msg.author.bot) return;

  let input = msg.content.trim();
  let isSudo = input.startsWith("sudo ");
  let command = isSudo ? input.slice(5) : input;

  const reply = (text) => msg.reply("```bash\n" + text + "\n```");

  // SUDO CHECK
  if (isSudo && !SUDO_USERS.includes(msg.author.id)) {
    return reply(
      `${msg.author.username} is not in the sudoers file.\nThis incident will be reported.`
    );
  }

  // rm -rf /
  if (command === "rm -rf /") {
    return reply(
      "💀 ERROR: SYSTEM FILES DELETED\n💀 Kernel panic - not syncing\n💀 RIP"
    );
  }

  // ls
  if (command === "ls") {
    return reply((files[currentDir] || []).join("  "));
  }

  // pwd
  if (command === "pwd") {
    return reply(currentDir);
  }

  // whoami
  if (command === "whoami") {
    return reply(isSudo ? "root" : msg.author.username);
  }

  // cd
  if (command.startsWith("cd")) {
    let dir = command.split(" ")[1];
    let newDir = dir === ".."
      ? "/"
      : currentDir === "/"
      ? `/${dir}`
      : `${currentDir}/${dir}`;

    if (files[newDir]) {
      currentDir = newDir;
      return reply("");
    } else {
      return reply(`bash: cd: ${dir}: No such file or directory`);
    }
  }

  // cat
  if (command.startsWith("cat")) {
    let file = command.split(" ")[1];
    if (file === "secret.txt") {
      return reply("DO NOT READ THIS FILE 😡");
    }
    return reply(`cat: ${file}: Permission denied`);
  }

  // neofetch
  if (command === "neofetch") {
    return reply(`
OS: BelugaOS
Kernel: 5.99.99-beluga
Uptime: 2 minutes
Shell: bash
CPU: Discord Nitro i9
Memory: 9999MiB / 9999MiB
    `);
  }

  // apt install
  if (command.startsWith("apt install")) {
    let pkg = command.replace("apt install", "").trim();
    return reply(
      `Reading package lists...\nInstalling ${pkg}...\nDone.`
    );
  }

  // shutdown / reboot
  if (command === "shutdown" || command === "reboot") {
    return reply("System is going down NOW!");
  }

  // touch
  if (command.startsWith("touch")) {
    let file = command.split(" ")[1];
    files[currentDir].push(file);
    return reply("");
  }

  // rm
  if (command.startsWith("rm")) {
    let file = command.split(" ")[1];
    files[currentDir] = files[currentDir].filter(f => f !== file);
    return reply("");
  }

  // DEFAULT
  reply(`bash: ${command}: command not found`);
});

client.once("ready", () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.login(TOKEN);
const { Client, GatewayIntentBits } = require("discord.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const TOKEN = "YOUR_BOT_TOKEN";

// USERS WHO CAN ACTUALLY SUDO
const SUDO_USERS = ["123456789012345678"];

// FAKE FILE SYSTEM
let currentDir = "/";
let files = {
  "/": ["home", "etc", "root", "virus.exe"],
  "/home": ["beluga", "notes.txt"],
  "/home/beluga": ["secret.txt"],
};

// COMMAND HANDLER
client.on("messageCreate", async (msg) => {
  if (msg.author.bot) return;

  let input = msg.content.trim();
  let isSudo = input.startsWith("sudo ");
  let command = isSudo ? input.slice(5) : input;

  const reply = (text) => msg.reply("```bash\n" + text + "\n```");

  // SUDO CHECK
  if (isSudo && !SUDO_USERS.includes(msg.author.id)) {
    return reply(
      `${msg.author.username} is not in the sudoers file.\nThis incident will be reported.`
    );
  }

  // rm -rf /
  if (command === "rm -rf /") {
    return reply(
      "💀 ERROR: SYSTEM FILES DELETED\n💀 Kernel panic - not syncing\n💀 RIP"
    );
  }

  // ls
  if (command === "ls") {
    return reply((files[currentDir] || []).join("  "));
  }

  // pwd
  if (command === "pwd") {
    return reply(currentDir);
  }

  // whoami
  if (command === "whoami") {
    return reply(isSudo ? "root" : msg.author.username);
  }

  // cd
  if (command.startsWith("cd")) {
    let dir = command.split(" ")[1];
    let newDir = dir === ".."
      ? "/"
      : currentDir === "/"
      ? `/${dir}`
      : `${currentDir}/${dir}`;

    if (files[newDir]) {
      currentDir = newDir;
      return reply("");
    } else {
      return reply(`bash: cd: ${dir}: No such file or directory`);
    }
  }

  // cat
  if (command.startsWith("cat")) {
    let file = command.split(" ")[1];
    if (file === "secret.txt") {
      return reply("DO NOT READ THIS FILE 😡");
    }
    return reply(`cat: ${file}: Permission denied`);
  }

  // neofetch
  if (command === "neofetch") {
    return reply(`
OS: BelugaOS
Kernel: 5.99.99-beluga
Uptime: 2 minutes
Shell: bash
CPU: Discord Nitro i9
Memory: 9999MiB / 9999MiB
    `);
  }

  // apt install
  if (command.startsWith("apt install")) {
    let pkg = command.replace("apt install", "").trim();
    return reply(
      `Reading package lists...\nInstalling ${pkg}...\nDone.`
    );
  }

  // shutdown / reboot
  if (command === "shutdown" || command === "reboot") {
    return reply("System is going down NOW!");
  }

  // touch
  if (command.startsWith("touch")) {
    let file = command.split(" ")[1];
    files[currentDir].push(file);
    return reply("");
  }

  // rm
  if (command.startsWith("rm")) {
    let file = command.split(" ")[1];
    files[currentDir] = files[currentDir].filter(f => f !== file);
    return reply("");
  }

  // DEFAULT
  reply(`bash: ${command}: command not found`);
});

client.once("ready", () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.login(TOKEN);
