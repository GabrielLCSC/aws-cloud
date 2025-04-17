import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import Apod from '@/views/Apod.vue'
import * as api from '@aws-amplify/api-rest'

vi.mock('@aws-amplify/api-rest')

describe('Apod.vue', () => {
  const mockData = [
    {
      date: '2024-04-17',
      title: 'La Terre vue de la Lune',
      mediaType: 'image',
      imageUrl: 'https://example.com/image.jpg',
      description: 'Une image fascinante prise depuis la Lune.',
      copyright: 'NASA',
    }
  ]

  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('affiche correctement les données APOD', async () => {
    vi.spyOn(api, 'get').mockResolvedValue({
      response: {
        body: {
          json: async () => mockData
        }
      }
    })

    const wrapper = mount(Apod)

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(wrapper.text()).toContain(mockData[0].title)
    expect(wrapper.text()).toContain(mockData[0].description)
    expect(wrapper.find('img').attributes('src')).toBe(mockData[0].imageUrl)
  })

  it('gère les erreurs d’API correctement', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
    vi.spyOn(api, 'get').mockRejectedValue(new Error('Erreur API'))

    mount(Apod)

    await new Promise(resolve => setTimeout(resolve, 0))

    expect(errorSpy).toHaveBeenCalled()
  })
})
