import { mount } from '@vue/test-utils'
import Fortune from '@/components/fortune.vue'

describe('Fortune', () => {
  test('is a Vue instance', () => {
    const wrapper = mount(Fortune)
    expect(wrapper.isVueInstance()).toBeTruthy()
  })
})
