// BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

#include <iostream>
#include <vector>

#include "awkward/Slice.h"
#include "awkward/fillable/FillableArray.h"
#include "awkward/fillable/FillableOptions.h"

namespace ak = awkward;

int main(int, char**) 
{

  // create fillable array
  ak::FillableArray myarray(ak::FillableOptions(1024, 2.0));

  // populate fillable array with lists
  myarray.beginrecord();
  myarray.field_check("one");
  myarray.boolean(true);
  myarray.field_check("two");
  myarray.integer(1);
  myarray.field_check("three");
  myarray.real(1.1);
  myarray.endrecord();
  
  myarray.beginrecord();
  myarray.field_check("one");
  myarray.boolean(false);
  myarray.field_check("two");
  myarray.integer(2);
  myarray.field_check("three");
  myarray.real(2.2);
  myarray.endrecord();

  myarray.beginrecord();
  myarray.field_check("one");
  myarray.boolean(true);
  myarray.field_check("two");
  myarray.integer(3);
  myarray.field_check("three");
  myarray.real(3.3);
  myarray.endrecord();

  // take a snapshot 
  std::shared_ptr<ak::Content> array = myarray.snapshot();

  // check output 
  if (array.get()->tojson(false,1) != "[{\"one\":true,\"two\":1,\"three\":1.1},{\"one\":false,\"two\":2,\"three\":2.2},{\"one\":true,\"two\":3,\"three\":3.3}]")
    {return -1;}
  return 0;
}


