import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { VoterApiService } from './voters/voter-api.service';
import { Voter } from './voters/voter.model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  votersListSubs: Subscription;
  votersList: Voter[];
  
  constructor(private votersApi: VoterApiService) {
  }
  
  ngOnInit() {
		this.votersListSubs = this.votersApi.getVoters().subscribe(res => {
			this.votersList = res;
		},
		console.error
	  );
  }
	  
  ngOnDestroy() {
	  this.votersListSubs.unsubscribe();
  }
}
