import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class GameSocketService {

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

  public joinGame() {
    this.socket.emit('joinGame', 'blah');
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
  public getTrivia() {
    return this.socket.fromEvent('create_trivia');
  }
}
