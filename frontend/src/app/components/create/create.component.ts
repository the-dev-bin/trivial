import { HttpClient } from '@angular/common/http';
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

  constructor(private gameSocket: GameSocketService, private httpClient: HttpClient) { }
  ngOnInit(): void {
    this.gameSocket.getTrivia().subscribe(data => {
      this.gameSocket.setUID(data.obj.uid)
    })
    this.httpClient.get('http://localhost:8000/gen').subscribe(data => {
      this.gameControl.setValue(JSON.stringify(data))
    })
  }
  gameControl = new FormControl('');
  public createTrivia() {
    this.gameSocket.createTrivia(this.gameControl.value);
  }
  
}
