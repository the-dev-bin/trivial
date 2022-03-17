import { Component, OnInit } from '@angular/core';
import { GameSocketService } from 'src/app/services/game-socket.service';

@Component({
  selector: 'app-host',
  templateUrl: './host.component.html',
  styleUrls: ['./host.component.scss']
})
export class HostComponent implements OnInit {

  constructor(private gameClient: GameSocketService) { }
  public trivia: any;
  public questions = ['a', 'b', 'c', 'd']
  ngOnInit(): void {
    
  }

}
