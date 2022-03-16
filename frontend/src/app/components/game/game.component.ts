import { Component, OnInit } from '@angular/core';
import { GameSocketService } from 'src/app/services/game-socket.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  constructor(private socketThing: GameSocketService) { }

  ngOnInit(): void {
    this.socketThing.getMessages().subscribe((data) => {
      console.log(data);
    })
  }
  public test() {
    this.socketThing.sendMessage();
  }
}
