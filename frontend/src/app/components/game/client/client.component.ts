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
    this.gameSocket.loginReturn().subscribe(data => {
      console.log(data.user);
      this.name = data.user.name;
    })
  }
  handleClick(answer: string) {
    console.log(answer);
  }

}
