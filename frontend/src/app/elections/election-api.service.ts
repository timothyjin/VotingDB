import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map, catchError} from 'rxjs/operators';
import {API_URL} from '../env';
import {Election} from './election.model';

@Injectable()
export class ElectionApiService {
	constructor(private http: HttpClient) {
	}
	
	private static _handleError(err: HttpErrorResponse | any){
		throw new Error(err.message || 'Error: Unable to complete request.');
	}
	
	getElections(): Observable<Election[]>{
		return this.http.get<Election[]>(`${API_URL}/elections`);
	}
	
	//getElections(year): Observable<Election[]>{
		//return this.http.get<Election[]>('${API_URL}/elections');
	//}
}