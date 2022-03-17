import { Component, OnInit } from '@angular/core';
import { map, Observable } from 'rxjs';
import { GameSocketService } from 'src/app/services/game-socket.service';

@Component({
  selector: 'app-host',
  templateUrl: './host.component.html',
  styleUrls: ['./host.component.scss']
})
export class HostComponent implements OnInit {

  constructor(private gameClient: GameSocketService) { }
  public trivia: any;
  public question$ = this.gameClient.setQuestionResponse();
  public gameID = this.gameClient.gameStart().pipe(map(data=>{    this.gameClient.joinGame(data.game_id); return data.game_id;}));
  public things:any = {

  }
  ngOnInit(): void {
    this.gameClient.startGame();
    this.gameClient.answerResponse().subscribe(data => {this.things[data.user_id] = data.answer});
  }
  public getGame() {
  }
  public advanceQuestion() {
    this.gameClient.advanceQuestion();
  }


}
