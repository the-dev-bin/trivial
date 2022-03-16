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
  ngOnInit(): void {
    this.gameSocket.login();
  }
  handleClick(answer: string) {
    console.log(answer);
  }

}
