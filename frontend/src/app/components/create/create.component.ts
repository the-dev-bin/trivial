import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { map } from 'rxjs';
import { GameSocketService } from 'src/app/services/game-socket.service';

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss']
})
export class CreateComponent implements OnInit {

  constructor(private gameSocket: GameSocketService) { }
  ngOnInit(): void {
    this.gameSocket.getTrivia().subscribe(data => {
      console.log(data);
    })
  }
  gameControl = new FormControl('');
  public createTrivia() {
    console.log(this.gameControl.value)
    this.gameSocket.createTrivia(this.gameControl.value);
  }

}
