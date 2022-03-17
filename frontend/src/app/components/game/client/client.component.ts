import { Component, OnInit } from '@angular/core';
import { GameSocketService } from 'src/app/services/game-socket.service';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.scss']
})
export class ClientComponent implements OnInit {

  constructor(private gameSocket: GameSocketService) { }
  public name = "";
  public question$ = this.gameSocket.setQuestionResponse();
  ngOnInit(): void {
    this.gameSocket.login();
    this.gameSocket.joinGame('foo');
  }
  handleClick(answer: number) {
    console.log(answer);
    this.gameSocket.answer(answer);
  }

}
