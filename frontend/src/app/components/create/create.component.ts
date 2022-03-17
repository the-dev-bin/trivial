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
      this.gameSocket.setUID(data.obj.uid)
    })
  }
  gameControl = new FormControl('');
  public createTrivia() {
    this.gameSocket.createTrivia(this.gameControl.value);
  }
  
}
