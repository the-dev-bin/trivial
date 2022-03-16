import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { GameComponent } from './components/game/game.component';
import { CreateComponent } from './components/create/create.component';
import { HomeComponent } from './components/home/home.component';

import { MatToolbarModule } from "@angular/material/toolbar";
import { SocketIoModule, SocketIoConfig} from 'ngx-socket-io';
 
const config : SocketIoConfig = { url: 'http://localhost:8000/sio/', options: {path: '/sio/socket.io/'} };

@NgModule({
  declarations: [
    AppComponent,
    GameComponent,
    CreateComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    SocketIoModule.forRoot(config) 
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
