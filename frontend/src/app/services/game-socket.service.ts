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
}
