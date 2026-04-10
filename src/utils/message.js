import { createVNode, render } from 'vue'
import MessageComponent from '../components/common/Message.vue'

let instance = null

const initInstance = () => {
  if (instance) return instance
  
  const container = document.createElement('div')
  document.body.appendChild(container)
  
  const vnode = createVNode(MessageComponent)
  render(vnode, container)
  
  instance = vnode.component.exposed
  return instance
}

export const Message = {
  success(content, duration = 3000) {
    const inst = initInstance()
    inst.addMessage({ type: 'success', content, duration })
  },
  error(content, duration = 3000) {
    const inst = initInstance()
    inst.addMessage({ type: 'error', content, duration })
  },
  warning(content, duration = 3000) {
    const inst = initInstance()
    inst.addMessage({ type: 'warning', content, duration })
  },
  info(content, duration = 3000) {
    const inst = initInstance()
    inst.addMessage({ type: 'info', content, duration })
  }
}
