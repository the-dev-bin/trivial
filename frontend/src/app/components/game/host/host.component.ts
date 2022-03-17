import { Component, OnInit } from '@angular/core';
import { map, Observable } from 'rxjs';
import { GameSocketService } from 'src/app/services/game-socket.service';
import { Player } from '../../../models/player.model'; 
@Component({
  selector: 'app-host',
  templateUrl: './host.component.html',
  styleUrls: ['./host.component.scss']
})
export class HostComponent implements OnInit {

  constructor(private gameClient: GameSocketService) { }
  public trivia: any;
  public people: {
    [uid: string]: Player
  } = {};
  public question$ = this.gameClient.setQuestionResponse();
  public gameID = this.gameClient.gameStart().pipe(map(data=>{    this.gameClient.joinGame(data.game_id); return data.game_id;}));
  public answers : {
    [uid: string]: number
  } = {

  }
  ngOnInit(): void {
    this.gameClient.startGame();
    this.gameClient.answerResponse().subscribe(data => {console.log(data);this.answers[data.user_id] = data.answer});
    this.gameClient.playerJoined().subscribe(player => {
      console.log(player)
      this.people[player.user.uid] = player;
      console.log(this.people)

    })
  }
  public getGame() {
  }
  public advanceQuestion() {
    this.gameClient.advanceQuestion();
  }


}
