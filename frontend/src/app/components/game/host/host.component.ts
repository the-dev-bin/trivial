import { Component, OnInit } from '@angular/core';
import { map, Observable } from 'rxjs';
import { GameSocketService } from 'src/app/services/game-socket.service';
import { Player } from '../../../models/player.model'; 
import { timer } from 'rxjs';

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
  public timeLeft = 0;
  public question$ = this.gameClient.setQuestionResponse();
  public gameID = this.gameClient.gameStart().pipe(map(data=>{    this.gameClient.joinGame(data.game_id); return data.game_id;}));
  public answers : {
    [question_number: number]: Player[]
  } = {}
  public correctAnswer : number | undefined = -1;
  public showAnswer = false;
  public gameEnd$ = this.gameClient.gameEnd();
  public timer: any;
  ngOnInit(): void {
    this.gameClient.startGame();
    this.gameClient.answerResponse().subscribe(data => {
      if(this.timeLeft <= 0) {
        return;
      }
      console.log(data);
      for (const [key, value] of Object.entries(this.answers)) {
        console.log(`${key}: ${value}`);
        this.answers[+key] = value.filter((answer) => {
          return answer.user.uid !== data.user_id;
        })
      }
      if(!this.answers[data.answer]){
        this.answers[data.answer] = [];
      }
      this.answers[data.answer].push(this.people[data.user_id]);;
    });
    this.gameClient.playerJoined().subscribe(player => {
      console.log(player)
      this.people[player.user.uid] = player;
      console.log(this.people)

    });
    this.gameClient.playerLeft().subscribe(player => {
      delete this.people[player.user_id]
    })
    this.gameClient.setQuestionResponse().subscribe(data => {
      this.answers = {};
      this.showAnswer = false;
      this.correctAnswer = data.question.choices.find(x=> x.correct)?.id
      this.timeLeft = 10;
    })
  }
  public getGame() {
  }
  public advanceQuestion() {
    this.timer?.unsubscribe();
    this.gameClient.advanceQuestion();
    this.timer = timer(1000, 1000).subscribe(() => {
      this.timeLeft--;
      if(this.timeLeft === 0) {
        this.showAnswer = true;
        this.timer.unsubscribe();
      }
    });
  }
  public startGame() {
    this.advanceQuestion();
  }

}
