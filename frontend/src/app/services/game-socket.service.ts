import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Player } from '../models/player.model';
import { Answer } from '../models/answer.model';
import { TriviaGame } from '../models/game.model';
@Injectable({
  providedIn: 'root'
})
export class GameSocketService {
  public uid: string = '';
  constructor(private socket: Socket) { }
  public sendMessage() {
    this.socket.emit('chat message', 'hello world')
  }
  public getMessages(): Observable<any> {
    return this.socket.fromEvent('chat message')
  }
  public login(): Observable<any> {
    return this.socket.emit('login')
  }
  public loginReturn(): Observable<{
    "status": string,
    "user": {
      name: string,
      picture: string
    }
}> {
    return this.socket.fromEvent('login');
  }

  public joinGame(room: string) {
    this.socket.emit('join', {
      game: room
    });
  }

  public choiceChange(): Observable<any> {
    return this.socket.fromEvent('change');
  }
  public changeChoice() {
    this.socket.emit('change');
  }
  public getQuestions() {
    this.socket.fromEvent('newAnswers');
  }

  public createTrivia(game: string) {
    this.socket.emit('create_trivia', JSON.parse(game));
  }
  public getTrivia(): Observable<{
    "status": string,
    "obj": {
        "uid": string,
        "name": string,
    }
}> {
    return this.socket.fromEvent('create_trivia');
  }
  
  public setUID(id: string) {
    this.uid = id;
  }
  public startGame() {
    this.socket.emit('start_game', {
      "trivia_id": this.uid
    })
  }
  public gameStart(): Observable<{
    status: string,
    game_id: string
  }> {
    return this.socket.fromEvent('start_game');
  }

  public advanceQuestion() {
    this.socket.emit('advance_question', {});
  }


  public setQuestionResponse(): Observable<TriviaGame> {
    return this.socket.fromEvent('set_question');
  }

  public answer(thing: number) {
    this.socket.emit('submit_answer', {
      game: 'foo',
      answer: thing
    })
  }

  public answerResponse(): Observable<Answer> {
    return this.socket.fromEvent('set_answer');
  }

  public playerJoined(): Observable<Player> {
    return this.socket.fromEvent('add_player');
  }
  public playerLeft() : Observable<{"user_id": string}> {
    return this.socket.fromEvent('remove_player')
  }
  public gameEnd(): Observable<any> {
    return this.socket.fromEvent('game_scores');
  }
}
