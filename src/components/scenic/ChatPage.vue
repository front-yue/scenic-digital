<template>
  <div class="page-frame">
    <PageHeader title="智能问答" subtitle="INTELLIGENT Q&A" />

    <div class="chat-body">
      <div ref="chatListRef" class="chat-list">
        <div
          v-for="(msg, i) in chatStore.chatMessages"
          :key="msg.role + '-' + i"
          class="chat-row"
          :class="msg.role === 'user' ? 'user' : 'assistant'"
        >
          <div class="chat-bubble">
            <div v-if="msg.role === 'assistant'" class="bubble-avatar">
              <Bot class="avatar-icon" />
            </div>
            <div class="bubble-content">{{ msg.content }}</div>
          </div>
        </div>

        <div v-if="!chatStore.chatMessages.length" class="chat-empty">
          <Sparkles class="empty-icon" />
          <p>向数字向导提问，开启智慧导览</p>
        </div>
      </div>
    </div>

    <div class="chat-input-bar">
      <input
        v-model="chatMessage"
        type="text"
        placeholder="向数字导览员发送消息..."
        @keyup.enter="handleSendMessage"
      />
      <div
        class="send-btn"
        :class="{ disabled: isSending || !chatMessage.trim(), sending: isSending }"
        @click="handleSendMessage"
      >
        <Send class="send-icon" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { Send, Bot, Sparkles } from 'lucide-vue-next'
import { useAvatarStore } from '@/stores/avatar'
import { sendFayMessage } from '@/api/fay'
import { Message } from '@/utils/message'
import PageHeader from '@/components/scenic/PageHeader.vue'

// 复用数字人 store 的对话记录（FAY 实时对答写入此处）
const chatStore = useAvatarStore()

const chatMessage = ref('')
const isSending = ref(false)
const chatListRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatListRef.value) {
      chatListRef.value.scrollTop = chatListRef.value.scrollHeight
    }
  })
}

// 发送：写入用户消息 -> 转发给 FAY WebSocket（回复由 useFaySocket 监听并播报）
const handleSendMessage = async () => {
  if (!chatMessage.value.trim() || isSending.value) return
  const text = chatMessage.value.trim()

  isSending.value = true
  chatStore.addChatMessage('user', text)
  scrollToBottom()
  chatMessage.value = ''
  try {
    await sendFayMessage(text)
  } catch (error) {
    console.error('发送消息失败:', error)
    Message.error('消息发送失败')
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}

watch(() => chatStore.chatMessages.length, scrollToBottom)
onMounted(scrollToBottom)
</script>

<style scoped>
.page-frame {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
  gap: 16px;
}

.chat-body {
  flex: 1;
  min-height: 0;
  position: relative;
}

.chat-list {
  position: absolute;
  inset: 0;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  border: 1px solid rgba(45, 212, 191, 0.18);
  border-radius: 16px;
  background: rgba(2, 18, 24, 0.55);
  backdrop-filter: blur(6px);
}

.chat-list::-webkit-scrollbar { width: 4px; }
.chat-list::-webkit-scrollbar-track { background: rgba(45, 212, 191, 0.05); border-radius: 2px; }
.chat-list::-webkit-scrollbar-thumb { background: rgba(45, 212, 191, 0.25); border-radius: 2px; }

.chat-row {
  display: flex;
}

.chat-row.user { justify-content: flex-end; }
.chat-row.assistant { justify-content: flex-start; }

.chat-bubble {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  max-width: 82%;
}

.chat-row.user .chat-bubble { flex-direction: row-reverse; }

.bubble-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(45, 212, 191, 0.12);
  border: 1px solid rgba(45, 212, 191, 0.3);
  flex-shrink: 0;
}

.avatar-icon {
  width: 17px;
  height: 17px;
  color: #2dd4bf;
}

.bubble-content {
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.7;
  color: #e2e8f0;
}

.chat-row.user .bubble-content {
  background: rgba(45, 212, 191, 0.18);
  border: 1px solid rgba(45, 212, 191, 0.35);
  border-top-right-radius: 4px;
}

.chat-row.assistant .bubble-content {
  background: rgba(2, 12, 18, 0.65);
  border: 1px solid rgba(45, 212, 191, 0.15);
  border-top-left-radius: 4px;
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: rgba(226, 232, 240, 0.4);
  font-size: 14px;
}

.empty-icon {
  width: 32px;
  height: 32px;
  color: rgba(45, 212, 191, 0.4);
}

.chat-input-bar {
  display: flex;
  gap: 12px;
  height: 50px;
  flex-shrink: 0;
}

.chat-input-bar input {
  flex: 1;
  height: 100%;
  border: 1px solid rgba(45, 212, 191, 0.2);
  border-radius: 12px;
  background: rgba(2, 18, 24, 0.55);
  color: #f0fdfa;
  font-size: 14px;
  padding: 0 18px;
  outline: none;
  transition: all 0.25s ease;
}

.chat-input-bar input::placeholder {
  color: rgba(45, 212, 191, 0.4);
}

.chat-input-bar input:focus {
  border-color: rgba(45, 212, 191, 0.55);
  background: rgba(2, 28, 32, 0.7);
  box-shadow: 0 0 18px rgba(45, 212, 191, 0.12);
}

.send-btn {
  width: 50px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(45, 212, 191, 0.15);
  border: 1px solid rgba(45, 212, 191, 0.35);
  color: #2dd4bf;
  cursor: pointer;
  transition: all 0.25s ease;
}

.send-btn:hover:not(.disabled) {
  background: rgba(45, 212, 191, 0.28);
  border-color: rgba(45, 212, 191, 0.6);
  box-shadow: 0 0 18px rgba(45, 212, 191, 0.2);
}

.send-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.send-btn.sending .send-icon {
  animation: pulse-send 1s ease-in-out infinite;
}

.send-icon {
  width: 18px;
  height: 18px;
}

@keyframes pulse-send {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.15); opacity: 1; }
}
</style>
