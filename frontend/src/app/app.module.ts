import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { GameComponent } from './components/game/game.component';
import { CreateComponent } from './components/create/create.component';

import { MatToolbarModule } from "@angular/material/toolbar";
import { SocketIoModule, SocketIoConfig} from 'ngx-socket-io';
import { HomeComponent } from "./components/home/home.component";
import { HostComponent } from './components/game/host/host.component';
import { ClientComponent } from './components/game/client/client.component';
import { NavbarComponent } from './components/navbar/navbar.component';
 
const config : SocketIoConfig = { url: 'http://localhost:8000', options: {path: '/sio/socket.io/'} };

@NgModule({
  declarations: [
    AppComponent,
    GameComponent,
    CreateComponent,
    HomeComponent,
    HostComponent,
    GameComponent,
    ClientComponent,
    NavbarComponent
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
