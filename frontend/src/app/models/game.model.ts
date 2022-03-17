export interface TriviaGame {
    status: string,
    question: {
      uid: string,
      text: string,
      notes: string,
      choices: {
        id: number,
        text: string,
        correct: boolean
      }[]
    }
  }