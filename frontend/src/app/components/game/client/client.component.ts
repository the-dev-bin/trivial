import { Component, OnInit } from '@angular/core';
import { GameSocketService } from 'src/app/services/game-socket.service';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.scss']
})
export class ClientComponent implements OnInit {

  constructor(private gameSocket: GameSocketService) { }
  public name = "";
  public question$ = this.gameSocket.setQuestionResponse();
  public gameJoined = false;
  gameControl = new FormControl('');
  ngOnInit(): void {
    this.gameSocket.login();
  }
  joinGame() {
    this.gameSocket.joinGame(this.gameControl.value);
    this.gameJoined = true;
  }
  handleClick(answer: number) {
    console.log(answer);
    this.gameSocket.answer(answer);
  }

}
