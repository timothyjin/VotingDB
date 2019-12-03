import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map, catchError} from 'rxjs/operators';
import {API_URL} from '../env';
import {Voter} from './voter.model';

@Injectable()
export class VoterApiService {
	constructor(private http: HttpClient) {
	}
	
	private static _handleError(err: HttpErrorResponse | any){
		throw new Error(err.message || 'Error: Unable to complete request.');
	}
	
	getVoters(): Observable<Voter[]>{
		return this.http.get<Voter[]>('${API_URL}/voters');
	}
}