import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { VoterApiService } from './voter-api.service';
import { Voter } from './voter.model';

@Component({
  selector: 'voter-list',
  templateUrl: './voter.component.html',
  styleUrls: ['../app.component.css']
})
export class VoterComponent implements OnInit, OnDestroy {
  title = 'voter-list';
  votersListSubs: Subscription;
  votersList: Voter[];
  attributes: String[];
  
  constructor(private votersApi: VoterApiService) {
  }
  
  ngOnInit() {
		this.votersListSubs = this.votersApi.getVoters().subscribe(res => {
			this.votersList = res;
		},
		console.error
	  );
	  this.attributes = ["SSN", "name", "birthday", "gender", "ethnicity", "income", "party"];
  }
	  
  ngOnDestroy() {
	  this.votersListSubs.unsubscribe();
  }
}
