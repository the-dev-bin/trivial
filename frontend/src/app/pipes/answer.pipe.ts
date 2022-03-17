import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'decode'
})
export class AnswerPipe implements PipeTransform {

  transform(value: string, ...args: unknown[]): unknown {
    return decodeURI(value) ;
  }

}
