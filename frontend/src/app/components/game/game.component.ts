import { Component, OnInit } from '@angular/core';
import { GameSocketService } from 'src/app/services/game-socket.service';

import { Status } from '../../models/status.model'
@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})

export class GameComponent implements OnInit {

  constructor(private gameSocket: GameSocketService) { }
  public statuses = Status;
  public status?: Status;
  
  ngOnInit(): void {
    this.gameSocket.getMessages().subscribe((data) => {
      console.log(data);
    })
    
  }


  public test() {
    this.gameSocket.sendMessage();
  }
  public joinGame() {
    this.status = Status.Client;
  }
  public startGame() {
    this.status = Status.Host;
  }
}
